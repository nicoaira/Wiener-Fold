library(dplyr)
library(msa)
library(e1071)
library(tidyverse)


df <- read.csv('expar_dataset.txt', sep=' ')

df[, ]

cols.remove <- c('id','tm1', 'tm2', 'X.bonds')

df <- df[, ! names(df) %in% cols.remove, drop = F]

df <- df %>% filter(p90 != 0 & n10 != 0 & nchar(sequence) == 30)
df <- df %>% filter(grepl( 'CI,', results) | grepl( 'CII,', results) |
                      results == 'CI' | results == 'CII' )

df <- df[sample(1:nrow(df)), ]



min_p90 <- range(df$p90)[1]
max_p90 <- range(df$p90)[2]
range_p90 <- max_p90 - min_p90
p90_limit <- min_p90 + range_p90 *.3

min_diff <- range(df$diff)[1]
max_diff <- range(df$diff)[2]
range_diff <- max_diff - min_diff

diff_limit <- max_diff - range_diff *.4


p90_df <- df %>% filter(p90 < p90_limit)
diff_df <- df %>% filter(diff > diff_limit)

sequences_p90 = as.vector(p90_df$sequence)
sequences_diff = as.vector(diff_df$sequence)


pwm_p90 <- PWM(sequences_p90)
pwm_diff <- PWM(sequences_diff)

pwm_p90 <- pwm_p90[,1:14]
pwm_diff <- pwm_diff[,1:14]


pwm_p90_energy <- matrix(,4,NCOL(pwm_p90))
rownames(pwm_p90_energy) <- rownames(pwm_p90)

pwm_diff_energy <- matrix(,4,NCOL(pwm_diff))
rownames(pwm_diff_energy) <- rownames(pwm_diff_energy)


## Matriz de energías descripta en el paper

for (col in seq(NCOL(pwm_p90)))
{
  pwm_p90_energy[,col] = log(max(pwm_p90[,col])/pwm_p90[,col], base = exp(1))
}


for (col in seq(NCOL(pwm_diff)))
{
  pwm_diff_energy[,col] = log(max(pwm_diff[,col])/pwm_diff[,col], base = exp(1))
}



calc_score_p90 <- function(secuencia){
  
  seq_split <- as.list(unlist((strsplit(secuencia , split=""))))[1:14]
  
  
  seq_matrix <- matrix(0,4,NCOL(pwm_p90))
  rownames(seq_matrix) <- rownames(pwm_p90)
  
  i <- 1
  
  for (base in seq_split)
  {
    seq_matrix[base,i] <- 1
    i <- i+1
  }
  
  score <- sum(seq_matrix * pwm_p90_energy)
}


calc_score_diff <- function(secuencia){
  
  seq_split <- as.list(unlist((strsplit(secuencia , split=""))))[1:14]
  
  
  seq_matrix <- matrix(0,4,NCOL(pwm_p90))
  rownames(seq_matrix) <- rownames(pwm_p90)
  
  i <- 1
  
  for (base in seq_split)
  {
    seq_matrix[base,i] <- 1
    i <- i+1
  }
  
  score <- sum(seq_matrix * pwm_diff_energy)
}




df$p90_scores <- lapply(df$sequence, FUN = calc_score_p90)
df$p90_scores <- as.numeric(df$p90_scores)

df$diff_scores <- lapply(df$sequence, FUN = calc_score_diff)
df$diff_scores <- as.numeric(df$diff_scores)


df <- df %>% filter(grepl( 'CI,', results) | grepl( 'CII,', results) |
                                  results == 'CI' | results == 'CII' )

df <- df %>%
  mutate(class = if_else( grepl( 'CII', results), 1, 0))




x <- df[c('diff_scores', 'p90_scores')]
y <- df$class


model <- svm(x=x, y=y)

plot(model)



pred <- predict(model, x[,])

# df <- df %>%
#   mutate(pred_class = if_else( pred > 0.5, 1, 0))


df$prediction <- pred

pred_sum <- sum(df$pred_class == df$class)
print(pred_sum)
print(nrow(df))

print(paste('Overall accuracy: ', round(pred_sum*100/nrow(df), 1), '%'))
