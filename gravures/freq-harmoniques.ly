\version "2.24.3"
%% Fichier produit par outils/generer.py — ne pas modifier à la main.
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
    \omit Staff.TimeSignature
    \cadenzaOn
    \accidentalStyle forget
    \clef bass
    c,1^\markup { \bold "1" }  c1^\markup { \bold "2" }  g1^\markup { \bold "3" }
    \clef treble
    c'1^\markup { \bold "4" }  e'1^\markup { \bold "5" } _\markup { \italic \small "-14" }  g'1^\markup { \bold "6" }  bes'1^\markup { \bold "7" } _\markup { \italic \small "-31" }  c''1^\markup { \bold "8" }  d''1^\markup { \bold "9" }  e''1^\markup { \bold "10" } _\markup { \italic \small "-14" }  fis''1^\markup { \bold "11" } _\markup { \italic \small "-49" }  g''1^\markup { \bold "12" }  aes''1^\markup { \bold "13" } _\markup { \italic \small "+41" }  bes''1^\markup { \bold "14" } _\markup { \italic \small "-31" }  b''1^\markup { \bold "15" } _\markup { \italic \small "-12" }  c'''1^\markup { \bold "16" }
    \bar "|."
  }
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/4)
    }
  }
}
