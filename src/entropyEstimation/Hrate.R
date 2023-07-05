# Load required libraries
library(Hrate)
library(getopt)

MAX_TOKENS <- 100000
STEP_SIZE <- 25 # 25 for fast mode, 100 for detailed mode

# Define the command line options
spec <- matrix(c(
  'tokens', 'T', 1, 'character',
  'output_dir', 'O', 1, 'character',
  'max_tokens', 'M', 1, 'integer',
  'fast', 'F', 1, 'integer'
), byrow = TRUE, ncol = 4)

args <- getopt(spec)

# Assign default values
file <- args$tokens
output_dir <- args$output_dir
max_tokens <- args$max_tokens
fast <- ifelse(is.null(args$fast), 0, args$fast)  # 0 for FALSE, 1 for TRUE
fast <- ifelse(fast == 0, FALSE, TRUE)

if (fast) {
  print('Using fast mode')
  STEP_SIZE <- 25
}


print(paste('File:', file))
print(paste('Output directory:', output_dir))
print(paste('Max tokens:', max_tokens))


# Main analysis
tokens <- readLines(file)
tokens <- PreprocessText(tokens, lower = FALSE, bow = TRUE)

if (max_tokens == 0) {
  max_tokens <- min(MAX_TOKENS, length(tokens))
} else {
  max_tokens <- min(max_tokens, length(tokens))
}

stabil <- stabilize.estimate(tokens, max.length = max_tokens, step.size = floor(max_tokens / STEP_SIZE), every.word = 10)

entropies <- get.stabilization(stabil)
sd <- get.criterion(stabil)

# Write the data frame to a CSV file
results <- data.frame(
  file = file,
  entropy = entropies,
  sd = sd
)

csv <- paste0(output_dir, '/hrate', ifelse(max_tokens != 0, paste0("_", max_tokens), ''), '.csv')
write.csv(results, csv, row.names = FALSE, col.names = TRUE)

# Plot the results
plot_file <- paste0(output_dir, '/hrate', ifelse(max_tokens != 0, paste0("_", max_tokens), ''), '.png')
png(plot_file)
plot(stabil)
dev.off()

plot_file <- paste0(output_dir, '/hrate_sd', ifelse(max_tokens != 0, paste0("_", max_tokens), ''), '.png')
png(plot_file)
plot.criterion(stabil)
dev.off()