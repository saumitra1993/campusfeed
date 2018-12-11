FROM openjdk:8-alpine

COPY target/uberjar/campusfeed.jar /campusfeed/app.jar

EXPOSE 3000

CMD ["java", "-jar", "/campusfeed/app.jar"]
