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
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \major d''2 d''2 \bar "|" cis''2 d''2 \bar "||" \key d \major e''2 d''2 \bar "|" cis''2 d''2 \bar "||" \key d \major d''2 d''2 \bar "|" cis''2 d''2 \bar "|." }
      \new Voice { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \major fis'2 g'2 \bar "|" g'2 fis'2 \bar "||" \key d \major g'2 fis'2 \bar "|" e'2 d'2 \bar "||" \key d \major fis'2 g'2 \bar "|" e'2 d'2 }
    >>
    \new Staff <<
      \clef bass
      \new Voice { \voiceOne \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \major a2 b2 \bar "|" a2 a2 \bar "||" \key d \major b2 a2 \bar "|" g2 fis2 \bar "||" \key d \major a2 b2 \bar "|" a2 fis2 }
      \new Voice = "basse" { \voiceTwo \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key d \major d2 g2 \bar "|" a2 d2 \bar "||" \key d \major g2 a2 \bar "|" a,2 d2 \bar "||" \key d \major d2 g,2 \bar "|" a,2 b,2 \bar "|." }
    >>
    \new Lyrics \lyricsto "basse" { \markup "I" \markup "IV" \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup "I" \markup \concat { "II" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "6" } } \markup \concat { "I" \hspace #0.15 \raise #0.55 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "6" "4" } } \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup "I" \markup "I" \markup "IV" \markup "V" \markup "VI" }
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
