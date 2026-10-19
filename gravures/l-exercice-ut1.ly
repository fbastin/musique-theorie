\version "2.24.3"
%% Fichier produit par outils/generer_lecture.py — ne pas modifier à la main.
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
  \new Staff {
    \clef soprano
    \omit Staff.TimeSignature
    \cadenzaOn
    c'1^\markup{\small 1} g'1^\markup{\small 2} c''1^\markup{\small 3} a1^\markup{\small 4} e'1^\markup{\small 5} e''1^\markup{\small 6} a'1^\markup{\small 7} d'1^\markup{\small 8} f''1^\markup{\small 9} b'1^\markup{\small 10} b1^\markup{\small 11} f'1^\markup{\small 12}
    \bar "|."
  }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #2.4 }
  }
}
