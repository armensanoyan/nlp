from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))

def create_friend_of(tx, name, friend):
    tx.run("MATCH (a:Person) WHERE a.name = $name "
           "CREATE (a)-[:KNOWS]->(:Person {name: $friend})",
           name=name, friend=friend)

def create_people(tx):
    tx.run("CREATE (a:Person {name:'Alice'})-[:KNOWS]->(:Person {name: 'Bob'})")

# with driver.session() as session:
#     session.write_transaction(create_people)

with driver.session() as session:
    session.write_transaction(create_friend_of, "Alice", "Heghie")

# with driver.session() as session:
#     session.write_transaction(create_friend_of, "Alice", "Carl")

driver.close()