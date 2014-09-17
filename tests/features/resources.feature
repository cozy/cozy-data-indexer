Feature: Index and search notes

    Scenario: Index and search note
        Given I index note through handlers with text "little stories begin"
        And I index note through handlers with text "great dragons are coming"
        And I index note through handlers with text "small hobbits are afraid"
        And I index note through handlers with text "such as humans"
        When I send a request to search the notes containing "dragons"
        Then this note is the second note I created

    Scenario: Index and search note with accents
        Given I index note through handlers with text "une leçon éclairante"
        And I index note through handlers with text "un ami aimé"
        And I index note through handlers with text "un élève discret"
        And I index note through handlers with text "danse avec les loups"
        When I send a request to search the notes containing "aimé"
        Then this note is the second note I created

    Scenario: Delete and search note
        Given I delete the second note index
        When I send a request to search the notes containing "dragons"
        Then there is no result
