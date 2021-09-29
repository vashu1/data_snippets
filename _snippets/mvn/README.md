
mvn archetype:generate -DarchetypeGroupId=org.apache.maven.archetypes -DarchetypeArtifactId=maven-archetype-quickstart -DarchetypeVersion=1.4

testGroup
testId

mvn install -DskipTests
mvn test
mvn test -Dtest=TestCircle#xyz

mvn exec:java -Dexec.mainClass="testGroup.App"

