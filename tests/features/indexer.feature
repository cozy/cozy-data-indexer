Feature: Indexing documents

    Scenario: Indexing notes
        Given I create five notes with tags and text
        And I index them
        When I ask for search "dragon"
        Then It returns me note "4" about "dragon"

    Scenario: Indexing notes and searching by tag
        Given I create five notes with tags and text
        And I index them
        When I ask for search "toto"
        Then It returns me notes "1,3" about "toto"

    Scenario: Removing notes
        Given I remove the note about "dragon"
        When I ask for search "dragon"
        Then It returns nothing

