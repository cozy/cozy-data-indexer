Feature: Indexing documents

    Scenario: Indexing notes
        Given I create five notes with tags and text
        And I index them
        When I ask for search "dragon"
        Then It returns me the note about "dragon"

    Scenario: Removing notes
        Given I remove the note about "dragon"
        When I ask for search "dragon"
        Then It returns nothing

