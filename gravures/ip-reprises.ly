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
      \clef treble \time 4/4 
      \set Score.barNumberVisibility = #all-bar-numbers-visible \override Score.BarNumber.break-visibility = #end-of-line-invisible \bar "" 
      \bar ".|:"
      e''4 d''4 c''4 d''4
      |
      e''4 e''4 e''2
      |
      \set Score.repeatCommands = #'((volta "1."))
      d''4 d''4 d''2
      \bar ":|."
      \set Score.repeatCommands = #'((volta #f) (volta "2."))
      c''1
      \set Score.repeatCommands = #'((volta #f))
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
