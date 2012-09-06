Feature: Index and search notes

    Scenario: Index and search note
        Given I index note through handlers with text "little stories begin"
        And I index note through handlers with text "great dragons are coming"
        And I index note through handlers with text "small hobbits are afraid"
        And I index note through handlers with text "such as humans"
        When I send a request to search the notes containing "dragons"
        Then this note is the second note I created

    Scenario: Delete and search note
        Given I delete the second note index
        When I send a request to search the notes containing "dragons"
        Then there is no result
