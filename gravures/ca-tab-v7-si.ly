\version "2.24.3"
%% Fichier produit par outils/generer_cadences.py — ne pas modifier à la main.
#(set-global-staff-size 13)
\paper {
  indent = 0
  ragged-right = ##f
  paper-width = 168\mm
  line-width = 166\mm
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
    \new Lyrics = "noms"
    \new Lyrics = "positions"
    \new Staff = "haut" { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "md" { \key b \major <dis' fis' b'>1 <e' fis' ais'>1 <dis' fis' b'>1 \bar "|"  <fis' b' dis''>1 <fis' ais' e''>1 <fis' b' dis''>1 \bar "|"  <b dis' fis'>1 <ais e' fis'>1 <b dis' fis'>1 \bar "||" \key b \minor <d' fis' b'>1 <e' fis' ais'>1 <d' fis' b'>1 \bar "|"  <fis' b' d''>1 <fis' ais' e''>1 <fis' b' d''>1 \bar "|"  <b d' fis'>1 <ais e' fis'>1 <b d' fis'>1 \bar "|." } }
    \new Staff { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key b \major b,1 fis1 b,1 \bar "|"  b,1 fis1 b,1 \bar "|"  b,1 fis1 b,1 \bar "||" \key b \minor b,1 fis1 b,1 \bar "|"  b,1 fis1 b,1 \bar "|"  b,1 fis1 b,1 \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { \markup \tiny \italic "si majeur" _ _ _ _ _ _ _ _ \markup \tiny \italic "si mineur" _ _ _ _ _ _ _ _ }
    \context Lyrics = "positions" \lyricsto "md" { \markup \tiny \italic "octave" _ _ \markup \tiny \italic "tierce" _ _ \markup \tiny \italic "quinte" _ _ \markup \tiny \italic "octave" _ _ \markup \tiny \italic "tierce" _ _ \markup \tiny \italic "quinte" _ _ }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #1.0
    }
    \context {
      \Lyrics
      \override LyricText.self-alignment-X = #LEFT
      \override LyricText.extra-spacing-width = #'(+inf.0 . -inf.0)
      \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #0.2
      \override VerticalAxisGroup.nonstaff-nonstaff-spacing.padding = #0.1
    }
  }
}
