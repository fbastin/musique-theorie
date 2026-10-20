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
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key e \minor e''2^\markup \small \italic \concat { "4" " " "—" " " "mi" " " "mineur" } e''2 \bar "|" dis''2 e''2 \bar "||" \key bes \major bes'2^\markup \small \italic \concat { "5" " " "—" " " "si" " " "bémol" " " "majeur" } c''2 \bar "|" a'2 \bar "||" \key c \minor d''2^\markup \small \italic \concat { "6" " " "—" " " "do" " " "mineur" } c''2 \bar "|" b'2 c''2 \bar "|." }
      \new Voice { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key e \minor g'2 a'2 \bar "|" fis'2 e'2 \bar "||" \key bes \major d'2 ees'2 \bar "|" c'2 \bar "||" \key c \minor f'2 ees'2 \bar "|" d'2 ees'2 }
    >>
    \new Staff <<
      \clef bass
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key e \minor b2 c'2 \bar "|" b2 g2 \bar "||" \key bes \major f2 g2 \bar "|" f2 \bar "||" \key c \minor aes2 g2 \bar "|" f2 ees2 }
      \new Voice = "basse" { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key e \minor e2 a,2 \bar "|" b,2 c2 \bar "||" \key bes \major bes,2 ees2 \bar "|" f2 \bar "||" \key c \minor f2 g2 \bar "|" g,2 c2 \bar "|." }
    >>

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
