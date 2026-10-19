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
      c''4 e''4 g''4 e''4
      |
      f''4 d''4 b'2
      \bar ":|."
      \textMark \markup \musicglyph "scripts.segno"
      c''4 c''4 e''4 g''4
      |
      \break
      c'''2 g''2
      \textEndMark \markup \italic "Fine" \bar "||"
      a''4 f''4 d''4 f''4
      |
      g''4 f''4 e''4 d''4
      \textEndMark \markup \italic "D.S. al Fine"
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
