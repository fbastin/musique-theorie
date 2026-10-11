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
    \clef bass
    \omit Staff.TimeSignature
    \cadenzaOn
    f1^\markup{\small 1} c1^\markup{\small 2} c'1^\markup{\small 3} g,1^\markup{\small 4} a1^\markup{\small 5} e,1^\markup{\small 6} e1^\markup{\small 7} a,1^\markup{\small 8} e'1^\markup{\small 9} d1^\markup{\small 10} g1^\markup{\small 11} f,1^\markup{\small 12}
    \bar "|."
  }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #2.4 }
  }
}
