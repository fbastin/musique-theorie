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
      <g'>1 <g' b'>1 <g' b' d''>1 <g' b' d'' f''>1
      \bar "|."
    }
    \addlyrics { "sol" "+ si" "+ ré" "+ fa" }
    \addlyrics { "fondamentale" "tierce" "quinte" "septième" }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #2.4
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }
}
