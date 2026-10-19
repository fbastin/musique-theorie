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
      <b' d'' g''>1^\markup \small "1" \bar "|" <g' bes' d''>1^\markup \small "2" \bar "|" <e' g' bes' c''>1^\markup \small "3" \bar "|" <gis' b' d'' f''>1^\markup \small "4" \bar "|" <f' bes' d''>1^\markup \small "5"
      \bar "|."
    }
    \addlyrics { "sol majeur" "ré mineur" "fa majeur" "la mineur" "si bémol majeur" }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #2.6
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }
}
