Feature: css3-fonts
 Scenario: font 030
   When launch "css3-fonts-app"
     And I go to "fonts/csswg/font-030-manual.htm"
     And I save the page to "font-030"
    Then pic "font-030" of baseline and result should be "100" similar if have results
