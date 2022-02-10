library(dplyr)
library(readxl)
library(janitor)
library(sf)
library(tidyverse)
library(ggplot2)
library(ggspatial)
library(dplyr)
library(lubridate)


source("/Users/jeferson/Documents/sisc/gestion_conocimiento/crime_mapping/functions.R")
source("/Users/jeferson/Documents/sisc/gestion_conocimiento/Sondeo_VIF/funciones.R")


data <- read_excel("/Users/jeferson/Documents/sisc/gestion_conocimiento/vsex_med/Archivo_plano_victima_202201290910_filter.xlsx")

data$year <- as.integer(year(data$fecha_ultimo_hecho))
data$mes <- month(data$fecha_ultimo_hecho)

data2 <- data[data$year >= 2018,]
data2$mes[data2$mes == 1] <- "Ene"
data2$mes[data2$mes == 2] <- "Feb"
data2$mes[data2$mes == 3] <- "Mar"
data2$mes[data2$mes == 4] <- "Abr"
data2$mes[data2$mes == 5] <- "May"
data2$mes[data2$mes == 6] <- "Jun"
data2$mes[data2$mes == 7] <- "Jul"
data2$mes[data2$mes == 8] <- "Ago"
data2$mes[data2$mes == 9] <- "Sep"
data2$mes[data2$mes == 10] <- "Oct"
data2$mes[data2$mes == 11] <- "Nov"
data2$mes[data2$mes == 12] <- "Dic"

conteo <- data2 %>%
  group_by(year, mes) %>%
  count()

ord <- c("Ene","Feb","Mar","Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")
conteo$mes<-factor(conteo$mes,levels=ord)
pal <- c('#191B4F','#1CA4C9','#511C71','#515151','#F9A61F','#178D4B','#AE3E92','#F77F11')


ggplot(data=conteo, aes(x=mes, y=n, group=as.character(year), color = as.character(year)))+
  geom_line(size=0.8, show.legend = F)+
  labs(title="Vsex por mes") +
  geom_point(size=2)+
  labs(colour = "Año")



##georef
coord_hom <- separate_lon_lat(data2, "punto_hecho")

homi_sf <- st_as_sf(coord_hom,coords = c('longitud', 'latitud') ,crs = 4326)

#Gráfico
ggplot()+
  annotation_map_tile()+
  geom_sf(data = homi_sf)


shp_name <- file.choose()
medellin_lsoa <- st_read(shp_name) # Se leyeron las formas de las comunas.
View(medellin_lsoa)

#Gráfico de shapes

ggplot()+
  geom_sf(data = medellin_lsoa)

new_object <- select(data2, codigo_comuna_hecho )
new_object <- na.omit(new_object)

count_crimes <- new_object %>%
  group_by(codigo_comuna_hecho) %>%
  summarise(total = n())

medellin_lsoa$COMUNA <- as.integer(medellin_lsoa$COMUNA)
count_crimes$codigo_comuna_hecho <- as.integer(count_crimes$codigo_comuna_hecho)

med_lsoa <- left_join(medellin_lsoa, count_crimes, by = c("COMUNA"="codigo_comuna_hecho"))


ggplot()+
  annotation_map_tile()+
  geom_sf(data = med_lsoa, aes(fill = total), alpha = 0.9)+
  scale_fill_gradient2(name ="Número de homicidios")
