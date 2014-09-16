Feature: pagination

    Scenario: backward-compatibility
        Given I index note through handlers with text "little stories begin"
        And I index note through handlers with text "great dragons are coming"
        And I index note through handlers with text "small hobbits are afraid"
        And I index note through handlers with text "such as humans"
        When I send a request to search the notes containing "dragon"
        Then this note is the second note I created

    Scenario: asking for the first page of results
        Given I index note through handlers with text "dragons stories begin with"
        And I index note through handlers with text "great dragons are coming"
        And I index note through handlers with text "small hobbits are afraid of dragons"
        And I index note through handlers with text "such as humans"
        When I search the notes containing "dragons" in page "1"
        Then the result should be the note "2"

    Scenario: asking for the first page of results
        Given I index note through handlers with text "little stories begin with dragons"
        And I index note through handlers with text "great dragons are coming"
        And I index note through handlers with text "small hobbits are afraid of dragons"
        And I index note through handlers with text "such as humans"
        When I search the notes containing "dragons" in page "2"
        Then the result should be the note "3"

    Scenario: asking for the first page of results
        Given I index note through handlers with text "little stories begin with dragons"
        And I index note through handlers with text "great dragons are coming"
        And I index note through handlers with text "small hobbits are afraid of dragons"
        And I index note through handlers with text "such as humans"
        When I search the notes containing "dragons" in page "3"
        Then the result should be the note "1"