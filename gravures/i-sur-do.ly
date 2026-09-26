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
  <<
    \new Staff {
      \accidentalStyle forget
      \clef treble \key c \major \omit Staff.TimeSignature \cadenzaOn
      <c' c'> <c' des'> <c' d'> <c' ees'> <c' e'> <c' f'> <c' fis'> \bar "" \break <c' ges'> <c' g'> <c' aes'> <c' a'> <c' bes'> <c' b'> <c' c''>
      \bar "|."
    }
    \addlyrics { "unisson" "2de m" "2de M" "3ce m" "3ce M" "4te J" "4te aug." "5te dim." "5te J" "6te m" "6te M" "7e m" "7e M" "8ve" }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #2.6
    }
    \context { \Lyrics \override LyricText.font-size = #-2.5 }
  }
}
