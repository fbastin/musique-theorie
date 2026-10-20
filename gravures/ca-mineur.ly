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
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key a \minor a'2^\markup \small \italic \concat { "parfaite" } a'2 \bar "|" gis'2 a'2 \bar "||" \key a \minor a'2^\markup \small \italic \concat { "rompue" } a'2 \bar "|" gis'2 a'2 \bar "|." }
      \new Voice { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key a \minor c'2 d'2 \bar "|" d'2 c'2 \bar "||" \key a \minor c'2 d'2 \bar "|" b2 a2 }
    >>
    \new Staff <<
      \clef bass
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key a \minor e2 f2 \bar "|" e2 e2 \bar "||" \key a \minor e2 f2 \bar "|" e2 c2 }
      \new Voice = "basse" { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key a \minor a,2 d2 \bar "|" e2 a,2 \bar "||" \key a \minor a,2 d,2 \bar "|" e,2 f,2 \bar "|." }
    >>
    \new Lyrics \lyricsto "basse" { \markup "I" \markup "IV" \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup "I" \markup "I" \markup "IV" \markup "V" \markup "VI" }
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
