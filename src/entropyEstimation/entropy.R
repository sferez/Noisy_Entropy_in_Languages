# Load required libraries
library(entropy)
library(ggplot2)
library(getopt)
library(sampling)

# Define the command line options
spec <- matrix(c(
  'tokens', 'T', 1, 'character',
  'output_dir', 'O', 1, 'character',
  'vocab', 'V', 1, 'character',
  'max_tokens', 'M', 1, 'integer',
  'bootstrap', 'B', 1, 'integer'
), byrow = TRUE, ncol = 4)

args <- getopt(spec)

# Assign default values
file <- args$tokens
output_dir <- args$output_dir
vocab <- ifelse(is.null(args$vocab), "NULL", args$vocab)
max_tokens <- ifelse(is.null(args$max_tokens), "NULL", args$max_tokens)
bootstrap <- ifelse(is.null(args$bootstrap), 0, args$bootstrap)  # 0 for FALSE, 1 for TRUE
bootstrap <- ifelse(bootstrap == 0, FALSE, TRUE)

print(paste('File:', file))
print(paste('Output directory:', output_dir))
print(paste('Vocab:', vocab))
print(paste('Max tokens:', max_tokens))
print(paste('Bootstrap:', bootstrap))


# Define constants
methods <- c('ML', 'MM', 'Laplace', 'CS', 'shrink', 'Jeffreys', 'SG', 'minimax')


# Function to calculate original entropy
original_entropy <- function(counts, method) {
  entropy(counts, method = method, unit = "log2")
}

# Function to perform bootstrap analysis
bootstrap_analysis <- function(tokens, vocab, n_bootstrap_samples = 100) {
  bootstrap_entropies <- list()
  for (method in methods) {
    bootstrap_entropies[[method]] <- numeric(n_bootstrap_samples)
  }

  for (i in 1:n_bootstrap_samples) {
    bootstrap_tokens <- sample(tokens, size = length(tokens), replace = TRUE)
    bootstrap_counts <- table(bootstrap_tokens)

    # Add 0 counts for vocab words not in bootstrap_tokens
    if (vocab != "NULL") {
      for (word in vocab) {
        if (!(word %in% names(bootstrap_counts))) {
          bootstrap_counts[word] <- 0
        }
      }
    }

    if (max_tokens != "NULL" && max_tokens < length(bootstrap_counts)) {
      stratum <- ifelse(bootstrap_counts > median(bootstrap_counts), "high", "low")
      size <- c(high = max_tokens * 0.6, low = max_tokens * 0.4)  # Adjust these proportions as needed
      strata_obj <- strata(data.frame(ID = names(bootstrap_counts), stratum = stratum), stratanames = "stratum", size = size, method = "srswor")
      bootstrap_counts <- bootstrap_counts[strata_obj$ID]
    }

    for (method in methods) {
      bootstrap_entropies[[method]][i] <- entropy(bootstrap_counts, method = method, unit = "log2")
    }
  }

  bootstrap_entropies
}

# Function to calculate statistical measures
cal_stats <- function(bootstrap_entropies, org_entropy) {
  mae <- mean(abs(bootstrap_entropies - org_entropy))
  mse <- mean((bootstrap_entropies - org_entropy)^2)
  sd <- sd(bootstrap_entropies)
  ci <- quantile(bootstrap_entropies, c(0.025, 0.975))  # 95% confidence interval
  list(mae = mae, mse = mse, sd = sd, ci = ci)
}

# Function to plot bootstrap entropy distribution
plot_fig <- function(bootstrap_entropies, org_entropy, method, ci, n_bootstrap_samples = 100) {
  df <- data.frame(Entropy = bootstrap_entropies)

  binwidth <- 2 * IQR(df$Entropy) / (length(df$Entropy)^(1 / 3))
  caption <- paste("Results over", n_bootstrap_samples, "bootstrap samples")
  if (max_tokens != "NULL") {
    caption <- paste(caption, "and with", max_tokens, "vocab words")
  }

  p <- ggplot(df, aes(x = Entropy)) +
    geom_histogram(aes(y = ..density..), fill = 'blue', color = 'black', alpha = 0.5, binwidth = binwidth) +
    geom_density(fill = 'blue', alpha = 0.2) +
    geom_vline(aes(xintercept = org_entropy, color = "Original Entropy"), linetype = 'dashed', size = 1.5) +
    geom_vline(aes(xintercept = ci[1], color = "95% CI"), linetype = 'dashed', size = 1) +
    geom_vline(aes(xintercept = ci[2], color = "95% CI"), linetype = 'dashed', size = 1) +
    labs(x = 'Entropy', y = 'Density', title = paste('Bootstrap Entropy Distribution (', method, ')'),
         caption = caption) +
    scale_color_manual(values = c("Original Entropy" = "red", "95% CI" = "green")) +
    theme_minimal()
  print(p)
}


# Main analysis
tokens <- readLines(file)
counts <- table(tokens)

# Add 0 counts for vocab words not in tokens
if (vocab != "NULL") {
  for (word in vocab) {
    if (!(word %in% names(counts))) {
      counts[word] <- 0
    }
  }
}

if (max_tokens != "NULL" && max_tokens < length(counts)) {
  stratum <- ifelse(counts > median(counts), "high", "low")
  size <- c(high = max_tokens * 0.6, low = max_tokens * 0.4)  # Adjust these proportions as needed
  strata_obj <- strata(data.frame(ID = names(counts), stratum = stratum), stratanames = "stratum", size = size, method = "srswor")
  counts <- counts[strata_obj$ID]
}

# Perform bootstrap analysis
if (bootstrap) {
  bootstrap_entropies <- bootstrap_analysis(tokens, vocab)
  results <- data.frame(
    file = character(),
    method = character(),
    entropy = numeric(),
    mae = numeric(),
    mse = numeric(),
    sd = numeric(),
    ci = character()
  )
} else {
  results <- data.frame(
    file = character(),
    method = character(),
    entropy = numeric()
  )
}

csv <- paste(output_dir, 'unigrams.csv', sep = '/')
write.csv(results, csv, row.names = FALSE, col.names = TRUE)


for (method in methods) {

  print(paste('Method:', method))

  # Calculate original entropy
  org_entropy <- original_entropy(counts, method)
  print(paste('Original entropy:', org_entropy))

  # Calculate statistical measures
  if (bootstrap) {
    stats <- cal_stats(bootstrap_entropies[[method]], org_entropy)
    print(paste('MAE:', stats$mae))
    print(paste('MSE:', stats$mse))
    print(paste('SD:', stats$sd))
    print(paste('95% CI:', paste(stats$ci, collapse = ', ')))
    results <- data.frame(
      file = file,
      method = method,
      entropy = org_entropy,
      mae = stats$mae,
      mse = stats$mse,
      sd = stats$sd,
      ci = paste0("[", stats$ci[1], ", ", stats$ci[2], "]")
    )
    # Plot bootstrap entropy distribution
    png(paste0(output_dir, '/', method, '.png'))
    plot_fig(bootstrap_entropies[[method]], org_entropy, method, stats$ci)
    dev.off()
  } else {
    results <- data.frame(
      file = file,
      method = method,
      entropy = org_entropy
    )
  }

  # Write the data frame to a CSV file
  write.table(results, csv, row.names = FALSE, col.names = FALSE, append = TRUE, sep = ',')
}
