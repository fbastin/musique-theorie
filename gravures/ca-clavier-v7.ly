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
    \new Staff { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major <e' g' c''>1^\markup \small \italic \concat { "do" " " "majeur" } <f' g' b'>1 <e' g' c''>1 \bar "||" \key a \major <cis' e' a'>1^\markup \small \italic \concat { "la" " " "majeur" } <d' e' gis'>1 <cis' e' a'>1 \bar "||" \key a \minor <c' e' a'>1^\markup \small \italic \concat { "la" " " "mineur" } <d' e' gis'>1 <c' e' a'>1 \bar "|." }
    \new Staff = "bas" { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "basse" { \key c \major c1 g1 c1 \bar "||" \key a \major a,1 e1 a,1 \bar "||" \key a \minor a,1 e1 a,1 \bar "|." } }
    \new Lyrics \lyricsto "basse" { \markup "I" \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup "I" \markup "I" \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup "I" \markup "I" \markup \concat { "V" \hspace #0.15 \raise #1.15 \fontsize #-3.5 \override #'(baseline-skip . 1.3) \column { "7" } } \markup "I" }
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
