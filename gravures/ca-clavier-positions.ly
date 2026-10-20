\version "2.24.3"
%% Fichier produit par outils/generer_cadences.py — ne pas modifier à la main.
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
  \new PianoStaff <<
    \new Staff { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major <e' g' c''>1^\markup \small \italic \concat { "position" " " "d'octave" } <f' a' c''>1 <d' g' b'>1 <e' g' c''>1 \bar "||" \key c \major <g' c'' e''>1^\markup \small \italic \concat { "position" " " "de" " " "tierce" } <a' c'' f''>1 <g' b' d''>1 <g' c'' e''>1 \bar "||" \key c \major <c' e' g'>1^\markup \small \italic \concat { "position" " " "de" " " "quinte" } <c' f' a'>1 <b d' g'>1 <c' e' g'>1 \bar "|." }
    \new Staff = "bas" { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "basse" { \key c \major c1 f1 g1 c1 \bar "||" \key c \major c1 f1 g1 c1 \bar "||" \key c \major c1 f1 g1 c1 \bar "|." } }
    \new Lyrics \lyricsto "basse" { \markup "I" \markup "IV" \markup "V" \markup "I" \markup "I" \markup "IV" \markup "V" \markup "I" \markup "I" \markup "IV" \markup "V" \markup "I" }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #1.9
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }
}
