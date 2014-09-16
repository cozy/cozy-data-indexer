Feature: Search by field

    Scenario: Searching in all fields
        Given I index note through handler with text "little stories begin", title "dragons story" and tag "story"
        And I index note through handler with text "great dragons are coming", title "great stories" and tag "story"
        And I index note through handler with text "small hobbits are afraid of dragons", title "hobbits" and tag "dragons"
        When I send a request to search the notes containing "dragon"
        Then all the notes should be in the results

    Scenario: Searching by title
        Given I index note through handler with text "little stories begin", title "dragons story" and tag "story"
        And I index note through handler with text "great dragons are coming", title "great stories" and tag "story"
        And I index note through handler with text "small hobbits are afraid of dragons", title "hobbits" and tag "dragons"
        When I search the notes containing "dragons" in "title" of type "string"
        Then the result should be note "1"

    Scenario: Searching by content
        Given I index note through handler with text "little stories begin", title "dragons story" and tag "story"
        And I index note through handler with text "great dragons are coming", title "great stories" and tag "story"
        And I index note through handler with text "small hobbits are afraid of dragons", title "hobbits" and tag "dragons"
        When I search the notes containing "dragons" in "content" of type "string"
        Then the result should be note "2"

    Scenario: Searching by description
        Given I index note through handler with text "little stories begin", title "dragons story" and tag "story"
        And I index note through handler with text "great dragons are coming", title "great stories" and tag "story"
        And I index note through handler with text "small hobbits are afraid of dragons", title "hobbits" and tag "dragons"
        When I search the notes containing "dragons" in "tags" of type ""
        Then the result should be note "3"