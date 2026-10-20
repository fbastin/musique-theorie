\version "2.24.3"
%% Fichier produit par outils/generer_interpretation.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new Staff  {
      \clef treble \time 4/4 \omit Staff.TimeSignature \cadenzaOn \override TextScript.staff-padding = #3 \textLengthOn
      c''4->-._\markup \small \italic \center-column { "accent" "et staccato" } \bar "|" c''4->--_\markup \small \italic \center-column { "accent" "et tenuto" } \bar "|" c''4-__\markup \small \italic \center-column { "tenuto" "et staccato" } \bar "|" c''4-^-._\markup \small \italic \center-column { "marcato" "et staccato" }
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
