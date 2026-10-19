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
      \clef treble \time 4/4 \tempo "Moderato" \override TextScript.staff-padding = #5.5
      c''4\p_\markup \small \bold 1 d''4 e''4 c''4 |
      c''4-._\markup \small \bold 2 d''4-. e''4-. c''4-. |
      e''4\<_\markup \small \bold 3 f''4 g''2\f_\markup \small \bold 4 |
      e''4(_\markup \small \bold 5 f''4) g''2->_\markup \small \bold 6 |
      \break g''8-^_\markup \small \bold 7 a''8 g''8 f''8 e''4 c''4 |
      g''8\>_\markup \small \bold 8 a''8 g''8 f''8 e''4 c''4--_\markup \small \bold 9 |
      c''4\pp_\markup \small \bold 10 g'4 c''2
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
