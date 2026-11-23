# Внешний Java-потребитель

Это самостоятельная Gradle-сборка, которая подключает только готовые JAR core и algorithms. Она не включена в пять производственных модулей, не использует исходники библиотек, JavaFX, application или io.

Нужен JDK 21. Из корня Student Lab:

```bash
./gradlew :fuzzy-core:jar :fuzzy-algorithms:jar
./gradlew -p examples/library-consumer clean run
```

Ожидаемый вывод:

```text
StudentParameters: center=10.0, scale=2.0, degreesOfFreedom=5
epsilon=0.001, membership(10)=1.0
alpha=0: [-3.4164, 23.4164]
alpha=1: [10.0000, 10.0000]
```

Пример создаёт `BoundedStudentFuzzyNumber` и вычисляет принадлежность в центре и два крайних α-сечения через публичный API `fuzzy-core`. JAR `fuzzy-algorithms` проверяется при подключении к classpath.

Для проверки полностью отдельно скопируйте каталог примера в другое место и передайте корень собранного Student Lab:

```bash
/absolute/path/to/fuzzy-quantities/gradlew -p /tmp/library-consumer \
  -PstudentLabLibraries=/absolute/path/to/fuzzy-quantities clean run
```

Можно обойтись без Gradle в самом примере. Для Linux/WSL из корня проекта, после сборки JAR:

```bash
mkdir -p examples/library-consumer/build/manual
javac --release 21 -encoding UTF-8 \
  -cp 'fuzzy-core/build/libs/fuzzy-core-0.1.0-SNAPSHOT.jar:fuzzy-algorithms/build/libs/fuzzy-algorithms-0.1.0-SNAPSHOT.jar' \
  -d examples/library-consumer/build/manual \
  examples/library-consumer/src/main/java/example/LibraryConsumer.java
java -cp 'examples/library-consumer/build/manual:fuzzy-core/build/libs/fuzzy-core-0.1.0-SNAPSHOT.jar:fuzzy-algorithms/build/libs/fuzzy-algorithms-0.1.0-SNAPSHOT.jar' \
  example.LibraryConsumer
```

В Windows используйте `gradlew.bat`; в ручном Java classpath разделителем служит `;`.
