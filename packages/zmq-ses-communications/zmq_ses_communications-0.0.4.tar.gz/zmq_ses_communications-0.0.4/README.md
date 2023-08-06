# zmq_ses_communications

Communication backend for integrating different entities in a facotry(robots, machines, web apps, database, humans, workstations).
Created using zmq sockets and protobuf.
There are two communication modes.

1. Broadcasting mode. Periodically send data to other entities.
2. Request/Response mode. Send request to a specific node and get a response.
