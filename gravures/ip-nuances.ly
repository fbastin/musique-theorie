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
      c''1\pp | c''1\p | c''1\mp | c''1\mf | c''1\f | c''1\ff
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
