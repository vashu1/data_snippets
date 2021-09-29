mvn archetype:generate \
  -DarchetypeGroupId=org.apache.camel.archetypes \
  -DarchetypeArtifactId=camel-archetype-java \
  -DarchetypeVersion=3.10.0

mvn install -DskipTests
mvn test
mvn test -Dtest=TestCircle#xyz

mvn install -DskipTests ; mvn camel:run
