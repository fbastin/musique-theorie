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
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \major d''2^\markup \small \italic \concat { "1" " " "—" " " "ré" " " "majeur" } d''2 \bar "|" cis''2 d''2 \bar "||" \key f \major f''2^\markup \small \italic \concat { "2" " " "—" " " "fa" " " "majeur" } e''2 \bar "|" f''2 \bar "||" \key g \major g'2^\markup \small \italic \concat { "3" " " "—" " " "sol" " " "majeur" } g'2 \bar "|" g'2 \bar "|." }
      \new Voice { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \major fis'2 g'2 \bar "|" g'2 fis'2 \bar "||" \key f \major a'2 g'2 \bar "|" f'2 \bar "||" \key g \major b2 c'2 \bar "|" b2 }
    >>
    \new Staff <<
      \clef bass
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \major a2 b2 \bar "|" a2 a2 \bar "||" \key f \major c'2 c'2 \bar "|" c'2 \bar "||" \key g \major d2 e2 \bar "|" d2 }
      \new Voice = "basse" { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \major d2 g2 \bar "|" a2 d2 \bar "||" \key f \major f2 c'2 \bar "|" a2 \bar "||" \key g \major g,2 c2 \bar "|" g,2 \bar "|." }
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
