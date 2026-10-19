\version "2.24.3"
%% Fichier produit par outils/generer_accords.py — ne pas modifier à la main.
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
  <<
    \new Staff {
      \accidentalStyle forget
      \clef treble \key c \major \omit Staff.TimeSignature \cadenzaOn
      <c' e' g'>1 <e' g' c''>1 <g' c'' e''>1
      \bar "|."
    }
    \addlyrics { "position fondamentale" "1er renversement" "2e renversement" }
    \addlyrics { \markup \fontsize #-1 \override #'(baseline-skip . 1.7) \center-column { "5" } \markup \fontsize #-1 \override #'(baseline-skip . 1.7) \center-column { "6" } \markup \fontsize #-1 \override #'(baseline-skip . 1.7) \center-column { "6" "4" } }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #3.4
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }
}
