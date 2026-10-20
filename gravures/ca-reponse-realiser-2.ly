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
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \minor e''2^\markup \small \italic \concat { "2" " " "—" " " "ré" " " "mineur" } d''2 \bar "|" cis''2 d''2 \bar "||" \key f \major f''2^\markup \small \italic \concat { "3" " " "—" " " "fa" " " "majeur" } g''2 \bar "|" e''2 f''2 \bar "|." }
      \new Voice { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \minor g'2 f'2 \bar "|" e'2 d'2 \bar "||" \key f \major a'2 bes'2 \bar "|" g'2 f'2 }
    >>
    \new Staff <<
      \clef bass
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \minor bes2 a2 \bar "|" a2 f2 \bar "||" \key f \major c'2 d'2 \bar "|" c'2 c'2 }
      \new Voice = "basse" { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \minor g2 a2 \bar "|" a,2 bes,2 \bar "||" \key f \major f2 bes2 \bar "|" c'2 a2 \bar "|." }
    >>
    \new Lyrics \lyricsto "basse" { \markup \concat { "II" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "6" } } \markup \concat { "I" \hspace #0.15 \raise #0.55 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "6" "4" } } \markup "V" \markup "VI" \markup "I" \markup \concat { "II" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "6" } } \markup "V" \markup \concat { "I" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "6" } } }
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
