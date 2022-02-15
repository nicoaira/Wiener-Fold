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


total_val <- 0
total_samples <- 0
contador <- 0

for (i in seq(1,nrow(df),nrow(df)/10)){
  
  
  contador <- contador + 1
  
  if (contador == 10){
    
    break
    
  }
  
  
  val_df <- df[i:(i+nrow(df)/10),]
  
  
  
  train_df <- df[-c(i:(i+nrow(df)/10)),]
  
  
  min_p90 <- range(train_df$p90)[1]
  max_p90 <- range(train_df$p90)[2]
  range_p90 <- max_p90 - min_p90
  p90_limit <- min_p90 + range_p90 *.3
  
  min_diff <- range(train_df$diff)[1]
  max_diff <- range(train_df$diff)[2]
  range_diff <- max_diff - min_diff
  
  diff_limit <- max_diff - range_diff *.4
  
  
  p90_df <- train_df %>% filter(p90 < p90_limit)
  diff_df <- train_df %>% filter(diff > diff_limit)
  
  all_sequences = as.vector(df$sequence)
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
  
  
  
  
  train_df$p90_scores <- lapply(train_df$sequence, FUN = calc_score_p90)
  train_df$p90_scores <- as.numeric(train_df$p90_scores)
  
  train_df$diff_scores <- lapply(train_df$sequence, FUN = calc_score_diff)
  train_df$diff_scores <- as.numeric(train_df$diff_scores)
  
  
  train_df <- train_df %>% filter(grepl( 'CI,', results) | grepl( 'CII,', results) |
                        results == 'CI' | results == 'CII' )
  
  train_df <- train_df %>%
    mutate(class = if_else( grepl( 'CII', results), 1, 0))
  
  
  
  
  x <- train_df[c('diff_scores', 'p90_scores')]
  y <- train_df$class
  
  
  
  model <- svm(x=x, y=y)
  
  print(paste('Contador', contador))
  
  
  plot(model)
  
  
  
  #### Validacion
  
  
  val_df$p90_scores <- lapply(val_df$sequence, FUN = calc_score_p90)
  val_df$p90_scores <- as.numeric(val_df$p90_scores)
  
  val_df$diff_scores <- lapply(val_df$sequence, FUN = calc_score_diff)
  val_df$diff_scores <- as.numeric(val_df$diff_scores)
  
  val_df <- val_df %>%
    mutate(class = if_else( grepl( 'CII', results), 1, 0))
  
  x_val <- val_df[c('diff_scores', 'p90_scores')]
  y_val <- val_df$class
  
  pred <- predict(model, x_val[,])
  
  val_df <- val_df %>%
    mutate(pred_class = if_else( pred > 0.5, 1, 0))
  
  
  val_sum <- sum(val_df$pred_class == val_df$class)
  
  print(paste('Val Acc #', contador, '=', round(val_sum*100/nrow(val_df), 1), '%'))
  
  total_val <- total_val + val_sum
  total_samples <- total_samples + nrow(val_df)
}

print(paste('Overall accuracy: ', round(total_val*100/total_samples, 2),'%'))


