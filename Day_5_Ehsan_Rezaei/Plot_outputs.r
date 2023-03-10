library(ggplot2)
library(raster)
library(rgdal)
library(sp)
library(reshape)


# Set working directory and read in data
data <- read.csv("C:/Users/rezaei/Desktop/monica_course_march_2023-main/out.csv")
data$AbBiom <- data$AbBiom / 1000

# Aggregate the biomass data
aggdata <-aggregate(data$AbBiom, by=list(data$year,data$sowing_doy,data$kg.N,data$mm.irrigation),FUN = median)

# change the column names
colnames(aggdata) <- c("Year", "Sowing_dates","Urea_amount","Irrigaiton","Biomass")



#Boxplot _ Irrigaiton
P1 = ggplot(aggdata, aes(x = as.factor(Irrigaiton), y = Biomass)) +
  geom_boxplot(notch = TRUE,color="blue") +
  geom_jitter(width = 0.2, alpha = 0.1,size=2) +
  labs(x = "Irrigation (mm)", y = "AG Biomass (t ha)")

P1

#Boxplot _ Urea amount
P2 = ggplot(aggdata, aes(x = as.factor(Urea_amount), y = Biomass)) +
  geom_boxplot(notch = TRUE,color="blue") +
  geom_jitter(width = 0.2, alpha = 0.1,size=2) +
  labs(x = "Urea amount (kg ha)", y = "AG Biomass (t ha)")

P2

#Boxplot _ Sowing date
 P3= ggplot(aggdata, aes(x = as.factor(Sowing_dates), y = Biomass)) +
  geom_boxplot(notch = TRUE,color="blue") +
  geom_jitter(width = 0.2, alpha = 0.1,size=2) +
  labs(x = "Sowing dates (DOY)", y = "AG Biomass (t ha)")

P3

###########mapping
# Aggregate the biomass data
aggdata_map <-aggregate(data$AbBiom, by=list(data$ID,data$sowing_doy,data$kg.N,data$mm.irrigation),FUN = median)

# change the column names
colnames(aggdata_map) <- c("ID","Sowing_dates","Urea_amount","Irrigaiton","Biomass")

# Replace label of treatments  
aggdata_map$Sowing_dates <- ifelse(aggdata_map$Sowing_dates == 244, "Early_sowing", aggdata_map$Sowing_dates)
aggdata_map$Sowing_dates <- ifelse(aggdata_map$Sowing_dates == 274, "Mid_sowing", aggdata_map$Sowing_dates)
aggdata_map$Sowing_dates <- ifelse(aggdata_map$Sowing_dates == 305, "Late_sowing", aggdata_map$Sowing_dates)
aggdata_map$Urea_amount <- ifelse(aggdata_map$Urea_amount == 100, "N50", aggdata_map$Urea_amount)
aggdata_map$Urea_amount <- ifelse(aggdata_map$Urea_amount == 200, "N100", aggdata_map$Urea_amount)
aggdata_map$Urea_amount <- ifelse(aggdata_map$Urea_amount == 400, "N200", aggdata_map$Urea_amount)
aggdata_map$Irrigaiton <- ifelse(aggdata_map$Irrigaiton == 0, "Rainfed", aggdata_map$Irrigaiton)
aggdata_map$Irrigaiton <- ifelse(aggdata_map$Irrigaiton == 100, "Sup_Irr", aggdata_map$Irrigaiton)


# merge the three columns with underscores in between
aggdata_map$SD_Urnit_Irr <- paste(aggdata_map$Sowing_dates, aggdata_map$Urea_amount, aggdata_map$Irrigaiton, sep = "_")

#Reading shape files
Grids= shapefile("D:/Dropbox/ZALF/MONICA_CR/Grids.shp")
ploygon = shapefile("D:/Dropbox/ZALF/MONICA_CR/Area.shp")
summary(ploygon)

merged_data <- merge(aggdata_map, Grids, by = "ID")


str(merged_data)
tiff("D:/Dropbox/ZALF/MONICA_CR/map.tiff"
     ,width = 3, height = 7, units = 'in', res = 300)

ggplot() +
  geom_raster(data = merged_data, aes(x = X_COORD, y = Y_COORD, fill = Biomass)) +
  geom_polygon(data = ploygon, aes(x=long, y=lat, group = group), 
               color = "black", fill = NA) +
  scale_fill_gradient2(low = "red",mid = "yellow", high = "blue") +
  facet_wrap(SD_Urnit_Irr ~ ., ncol = 3,strip.position = "left")+
  theme_void()+
  theme(strip.text = element_text(size = 5, angle = 90, hjust = 0)) 

dev.off()
