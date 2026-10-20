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
    \new Staff <<
      \clef treble
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major c''2^\markup \small \italic \concat { "depuis" " " "IV" } c''2 \bar "|" b'2 c''2 \bar "||" \key c \major d''2^\markup \small \italic \concat { "depuis" " " "la" " " "quarte" " " "et" " " "sixte" } c''2 \bar "|" b'2 c''2 \bar "|." }
      \new Voice { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major e'2 f'2 \bar "|" d'2 c'2 \bar "||" \key c \major f'2 e'2 \bar "|" d'2 c'2 }
    >>
    \new Staff <<
      \clef bass
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major g2 a2 \bar "|" g2 e2 \bar "||" \key c \major a2 g2 \bar "|" g2 e2 }
      \new Voice = "basse" { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major c2 f,2 \bar "|" g,2 a,2 \bar "||" \key c \major f2 g2 \bar "|" g,2 a,2 \bar "|." }
    >>
    \new Lyrics \lyricsto "basse" { \markup "I" \markup "IV" \markup "V" \markup "VI" \markup \concat { "II" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "6" } } \markup \concat { "I" \hspace #0.15 \raise #0.55 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "6" "4" } } \markup "V" \markup "VI" }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/4)
      \override SpacingSpanner.spacing-increment = #1.5
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }
}
