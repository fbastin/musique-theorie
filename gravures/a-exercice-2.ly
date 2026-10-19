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
      <a' dis'' fis'' b''>1^\markup \small "6" \bar "|" <ees' g' b'>1^\markup \small "7" \bar "|" <e' a' cis'' g''>1^\markup \small "8" \bar "|" <aes' c'' f''>1^\markup \small "9" \bar "|" <cis'' e'' g''>1^\markup \small "10"
      \bar "|."
    }
    \addlyrics { "mi mineur" "do mineur" "ré majeur" "mi bémol majeur" "si mineur" }
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
