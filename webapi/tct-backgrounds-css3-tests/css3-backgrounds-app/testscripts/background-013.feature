Feature: css3-backgrounds
 Scenario: background 013
   When launch "css3-backgrounds-app"
     And I go to "csswg/background-013-manual.htm"
     And I save the page to "background-013"
    Then pic "background-013" of baseline and result should be "100" similar if have results
