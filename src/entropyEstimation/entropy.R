# Load required libraries
library(entropy)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)

# Define constants
methods <- c('ML', 'MM', 'Laplace', 'CS', 'shrink', 'Jeffreys', 'SG', 'minimax')

# Read tokens and vocab from file
tokens <- readLines(args[1])
output_dir <- args[2]
if (length(args) >= 3) {
  vocab <- readLines(args[3])
} else {
  vocab <- NULL
}

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
    if (!is.null(vocab)) {
      for (word in vocab) {
        if (!(word %in% names(bootstrap_counts))) {
          bootstrap_counts[word] <- 0
        }
      }
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

  binwidth <- 2 * IQR(df$Entropy) / (length(df$Entropy)^(1/3))

  p <- ggplot(df, aes(x = Entropy)) +
    geom_histogram(aes(y = ..density..), fill = 'blue', color = 'black', alpha = 0.5, binwidth = binwidth) +
    geom_density(fill = 'blue', alpha = 0.2) +
    geom_vline(aes(xintercept = org_entropy, color = "Original Entropy"), linetype = 'dashed', size = 1.5) +
    geom_vline(aes(xintercept = ci[1], color = "95% CI"), linetype = 'dashed', size = 1) +
    geom_vline(aes(xintercept = ci[2], color = "95% CI"), linetype = 'dashed', size = 1) +
    labs(x = 'Entropy', y = 'Density', title = paste('Bootstrap Entropy Distribution (', method, ')'),
    caption = paste("Results over", n_bootstrap_samples, "bootstrap samples")) +
    scale_color_manual(values = c("Original Entropy" = "red", "95% CI" = "green")) +
    theme_minimal()
  print(p)
}


# Main analysis
counts <- table(tokens)

# Add 0 counts for vocab words not in tokens
if (!is.null(vocab)) {
  for (word in vocab) {
    if (!(word %in% names(counts))) {
      counts[word] <- 0
    }
  }
}

# bootstrap_entropies <- bootstrap_analysis(tokens, vocab)

csv <- paste(output_dir, 'results.csv', sep = '/')
# write csv header
results <- data.frame(
  file = character(),
  method = character(),
  entropy = numeric(),
  mae = numeric(),
  mse = numeric(),
  sd = numeric(),
  ci = character()
)
write.csv(results, csv, row.names = FALSE, col.names = TRUE)

# write.table(c('file', 'method', 'entropy', 'mae', 'mse', 'sd', 'ci'), file = paste(output_dir, 'result.csv', sep = '/'), row.names = FALSE, col.names = FALSE, sep = ',')

for (method in methods) {

  print(paste('Method:', method))

  # Calculate original entropy
  org_entropy <- original_entropy(counts, method)
  print(paste('Original entropy:', org_entropy))

  # # Calculate statistical measures
  # stats <- cal_stats(bootstrap_entropies[[method]], org_entropy)
  # print(paste('MAE:', stats$mae))
  # print(paste('MSE:', stats$mse))
  # print(paste('SD:', stats$sd))
  # print(paste('95% CI:', paste(stats$ci, collapse = ', ')))
  #
  # results <- data.frame(
  #   file = args[1],
  #   method = method,
  #   entropy = org_entropy,
  #   mae = stats$mae,
  #   mse = stats$mse,
  #   sd = stats$sd,
  #   ci = paste0("[", stats$ci[1], ", ", stats$ci[2], "]")
  # )
  #
  # # Write the data frame to a CSV file
  # write.table(results, csv, row.names = FALSE, col.names = FALSE, append = TRUE, sep = ',')
  #
  # # Plot bootstrap entropy distribution
  # png(paste0(output_dir, '/', method, '.png'))
  # plot_fig(bootstrap_entropies[[method]], org_entropy, method, stats$ci)
  # dev.off()

}
