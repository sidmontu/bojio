library(ggplot2)
library(ggthemes)
library(stringr)

data <- read.csv('stationary_results.csv', header = T, sep = ",", stringsAsFactors = F)
data$xlabel <- paste("",2**abs(data$power),sep="")
data$xlabel[data$power < 0] <- paste("1/",2**abs(data$power[data$power < 0]),sep="")
data$xlabel <- factor(data$xlabel, levels = c("1/128","1/64","1/32","1/16","1/8","1/4","1/2","1","2","4"))

data$method[data$method == 'epsilon-greedy'] <- "Epsilon-Greedy"
data$method[data$method == 'gradient-bandit'] <- "Gradient Bandit"
data$method[data$method == 'ucb'] <- "UCB"
data$method[data$method == 'opt-greedy'] <- "Greedy (optimistic initialization)"

pdf('stationary.pdf', width = 12, height = 7)
ggplot(data, aes(x=power,y=value,color=method)) +
    geom_point(size=3) +
    geom_line(size=2) +
    scale_x_continuous("Parameter values", breaks = unique(data$power), labels = unique(data$xlabel)) +
    scale_y_continuous(str_wrap("Average reward over first 1000 steps", width = 25)) +
	# scale_color_pander() +
	scale_color_tableau() +
	theme_minimal() +
  	theme(
		legend.position="top",
		legend.title=element_blank(),
		# legend.background = element_rect(fill="gray90"),
		legend.key=element_blank(),
		legend.key.width=unit(1,"cm"),
		legend.key.height=unit(1,"cm"),
		axis.text.x=element_text(size=18,angle=0,hjust=0.5,vjust=0),
		axis.text.y=element_text(size=18,angle=0,hjust=1),
		axis.title.x = element_text(size=24,angle=0,hjust=.5,vjust=0,face="plain"),
        axis.title.y = element_text(size=24,hjust=.5,vjust=.5,face="plain"),
        # panel.background = element_blank(),
        # panel.grid.major = element_blank(),
        # panel.grid.minor = element_blank(),
        axis.line = element_line(colour = "black"),
        panel.border = element_rect(colour = "black", fill=NA, size=1),
		legend.text=element_text(size=18)) +
	guides(
		color=guide_legend(ncol=4,nrow=1)
	) +
	theme(axis.line = element_line(color = 'black'))

data <- read.csv('nonstationary_results.csv', header = T, sep = ",", stringsAsFactors = F)
data$xlabel <- paste("",2**abs(data$power),sep="")
data$xlabel[data$power < 0] <- paste("1/",2**abs(data$power[data$power < 0]),sep="")
data$xlabel <- factor(data$xlabel, levels = c("1/128","1/64","1/32","1/16","1/8","1/4","1/2","1","2","4"))

data$method[data$method == 'epsilon-greedy'] <- "Epsilon-Greedy"
data$method[data$method == 'gradient-bandit'] <- "Gradient Bandit"
data$method[data$method == 'ucb'] <- "UCB"
data$method[data$method == 'opt-greedy'] <- "Greedy (optimistic initialization)"

pdf('nonstationary.pdf', width = 12, height = 7)
ggplot(data, aes(x=power,y=value,color=method)) +
    geom_point(size=3) +
    geom_line(size=2) +
    scale_x_continuous("Parameter values", breaks = unique(data$power), labels = unique(data$xlabel)) +
    scale_y_continuous(str_wrap("Average reward over last 100K steps", width = 25)) +
	# scale_color_pander() +
	scale_color_tableau() +
	theme_minimal() +
  	theme(
		legend.position="top",
		legend.title=element_blank(),
		# legend.background = element_rect(fill="gray90"),
		legend.key=element_blank(),
		legend.key.width=unit(1,"cm"),
		legend.key.height=unit(1,"cm"),
		axis.text.x=element_text(size=18,angle=0,hjust=0.5,vjust=0),
		axis.text.y=element_text(size=18,angle=0,hjust=1),
		axis.title.x = element_text(size=24,angle=0,hjust=.5,vjust=0,face="plain"),
        axis.title.y = element_text(size=24,hjust=.5,vjust=.5,face="plain"),
        # panel.background = element_blank(),
        # panel.grid.major = element_blank(),
        # panel.grid.minor = element_blank(),
        axis.line = element_line(colour = "black"),
        panel.border = element_rect(colour = "black", fill=NA, size=1),
		legend.text=element_text(size=18)) +
	guides(
		color=guide_legend(ncol=4,nrow=1)
	) +
	theme(axis.line = element_line(color = 'black'))
