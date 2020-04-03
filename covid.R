setwd('/home/eduardofv/local/eduardofv/varios/covid')
#https://ourworldindata.org/grapher/covid-confirmed-cases-since-100th-case?time=5..64&country=CAN+CRI+DOM+MEX+PAN+USA
d<-read.csv("covid-confirmed-cases-since-100th-case.csv")

compareCountries <- function(df, code1, code2, log=T){
  d1 <- df[df$Entity==code1,]
  d2 <- df[df$Entity==code2,]
  l <- c(code1, code2)
  if(max(d1$Days.since.the.total.confirmed.cases.of.COVID.19.reached.100, na.rm = T) < max(d2$Days.since.the.total.confirmed.cases.of.COVID.19.reached.100, na.rm = T)){
    d1 <- df[df$Entity==code2,]
    d2 <- df[df$Entity==code1,]
    l <- c(code2, code1)
  }
  is_log = ""
  if(log) 
    is_log = "y"
  plot(d1$Days.since.the.total.confirmed.cases.of.COVID.19.reached.100, 
       d1$Total.confirmed.cases.of.COVID.19..cases., 
       log=is_log,
       pch="o",
       type="l",
       col="blue")
  points(d1$Days.since.the.total.confirmed.cases.of.COVID.19.reached.100, 
       d1$Total.confirmed.cases.of.COVID.19..cases., 
       #log="y",
       pch="o",
       col="blue")
  lines(d2$Days.since.the.total.confirmed.cases.of.COVID.19.reached.100, 
         d2$Total.confirmed.cases.of.COVID.19..cases.,
         #log="y",
         pch="x",
         col="darkgreen")
  points(d2$Days.since.the.total.confirmed.cases.of.COVID.19.reached.100, 
         d2$Total.confirmed.cases.of.COVID.19..cases.,
         #log="y",
         pch="x",
         col="darkgreen")
  legend("bottomright", legend=l, col=c("blue", "green"), pch=c("o","x"))
}

compareCountries(d, "Mexico", "China")
#points(7,465,log="y",pch="x",col="green")