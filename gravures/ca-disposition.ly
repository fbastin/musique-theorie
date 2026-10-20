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
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major c''2^\markup \small \italic \concat { "do" " " "majeur" } c''2 \bar "|" b'2 c''2 \bar "||" \key bes \major bes'2^\markup \small \italic \concat { "si" " " "bémol" " " "majeur" } bes'2 \bar "|" a'2 bes'2 \bar "||" \key d \minor d''2^\markup \small \italic \concat { "ré" " " "mineur" } d''2 \bar "|" cis''2 d''2 \bar "|." }
      \new Voice { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major e'2 f'2 \bar "|" f'2 e'2 \bar "||" \key bes \major d'2 ees'2 \bar "|" ees'2 d'2 \bar "||" \key d \minor f'2 g'2 \bar "|" g'2 f'2 }
    >>
    \new Staff <<
      \clef bass
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major g2 a2 \bar "|" g2 g2 \bar "||" \key bes \major f2 g2 \bar "|" f2 f2 \bar "||" \key d \minor a2 bes2 \bar "|" a2 a2 }
      \new Voice = "basse" { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major c2 f2 \bar "|" g2 c2 \bar "||" \key bes \major bes,2 ees2 \bar "|" f2 bes,2 \bar "||" \key d \minor d2 g2 \bar "|" a2 d2 \bar "|." }
    >>
    \new Lyrics \lyricsto "basse" { \markup "I" \markup "IV" \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup "I" \markup "I" \markup "IV" \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup "I" \markup "I" \markup "IV" \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup "I" }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/4)
      \override SpacingSpanner.spacing-increment = #1.3
    }
    \context { \Lyrics \override LyricText.font-size = #-1.5
               \override LyricSpace.minimum-distance = #2 }
  }
}
