FROM eclipse-temurin:17

WORKDIR /app

COPY Server.java .

RUN javac Server.java

EXPOSE 5000

CMD ["java", "Server"]