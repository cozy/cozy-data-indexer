Feature: number of results

    Scenario: backward-compatibility
        Given I index note through handlers with text "little stories begin"
        And I index note through handlers with text "great dragons are coming"
        And I index note through handlers with text "small hobbits are afraid"
        And I index note through handlers with text "such as humans"
        When I send a request to search the notes containing "dragon"
        Then this note is the second note I created

    Scenario: asking for number of matched results
        Given I index note through handlers with text "little stories begin"
        And I index note through handlers with text "great dragons are coming"
        And I index note through handlers with text "small hobbits are afraid"
        And I index note through handlers with text "such as humans"
        When I search the notes containing "dragons" with option to show number of matched results
        Then the result is an object with fields, the notes and the number of results
        And then this note is the second note I created