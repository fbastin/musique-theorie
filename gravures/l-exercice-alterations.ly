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
    \clef treble
    \key f \major
    \omit Staff.TimeSignature
    \cadenzaOn
    \once \omit Accidental a'1^\markup{\small 1} \once \omit Accidental bes'1^\markup{\small 2} b'!1^\markup{\small 3} \once \omit Accidental b'1^\markup{\small 4} \once \omit Accidental c''1^\markup{\small 5} \bar "|" \once \omit Accidental bes'1^\markup{\small 6} gis'!1^\markup{\small 7} \once \omit Accidental a'1^\markup{\small 8} \once \omit Accidental gis'1^\markup{\small 9} \once \omit Accidental g''1^\markup{\small 10} \bar "|" ees''!1^\markup{\small 11} \once \omit Accidental d''1^\markup{\small 12} \once \omit Accidental ees''1^\markup{\small 13} \once \omit Accidental e'1^\markup{\small 14}
    \bar "|."
  }
  \layout { \context { \Score \override SpacingSpanner.spacing-increment = #1.5 } }
}
