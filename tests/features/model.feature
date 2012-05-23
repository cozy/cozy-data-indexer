Feature: Model management through API

    Scenario: Creation and existence
        Send a request to check existence of Note with id equal to 123
        Check that {exists: false} is returned
        Send a request to create a note
        Send a request to check existence of Note with id equal to note ID
        Check that {exists: true} is returned
    
