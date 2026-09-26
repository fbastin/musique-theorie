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
      <c' d'> <d' c''> <c' e'> <e' c''> <c' ees'> <ees' c''> <c' f'> <f' c''> <c' fis'> <fis' c''>
      \bar "|."
    }
    \addlyrics { "2de M" "7e m" "3ce M" "6te m" "3ce m" "6te M" "4te J" "5te J" "4te aug." "5te dim." }
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
