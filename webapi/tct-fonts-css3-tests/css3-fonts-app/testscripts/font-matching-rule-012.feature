Feature: css3-fonts
 Scenario: font matching rule 012
   When launch "css3-fonts-app"
     And I go to "fonts/csswg/font-matching-rule-012.xht"
     And I save the page to "font-matching-rule-012"
     And I save the screenshot md5 as "font-matching-rule-012"
    Then file "font-matching-rule-012" of baseline and result should be the same
