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
      \clef treble \time 4/4 \override TextScript.staff-padding = #3
      c''4(_\markup \small \italic "legato" d''4 e''4 f''4) |
      c''4-._\markup \small \italic "staccato" d''4-. e''4-. f''4-. |
      c''4-!_\markup \small \italic "staccatissimo" d''4-! e''4-! f''4-! |
      c''4-.(_\markup \small \italic "portato" d''4-. e''4-. f''4-.) |
      \break c''4--_\markup \small \italic "tenuto" d''4-- e''4-- f''4-- |
      c''4->_\markup \small \italic "accent" d''4-> e''4-> f''4-> |
      c''4-^_\markup \small \italic "marcato" d''4-^ e''4-^ f''4-^
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
