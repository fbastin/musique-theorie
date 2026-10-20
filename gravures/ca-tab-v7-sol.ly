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
    \new Staff = "haut" { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "md" { \key g \major <b d' g'>1 <c' d' fis'>1 <b d' g'>1 \bar "|"  <d' g' b'>1 <d' fis' c''>1 <d' g' b'>1 \bar "|"  <g' b' d''>1 <fis' c'' d''>1 <g' b' d''>1 \bar "||" \key g \minor <bes d' g'>1 <c' d' fis'>1 <bes d' g'>1 \bar "|"  <d' g' bes'>1 <d' fis' c''>1 <d' g' bes'>1 \bar "|"  <g' bes' d''>1 <fis' c'' d''>1 <g' bes' d''>1 \bar "|." } }
    \new Staff { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key g \major g,1 d1 g,1 \bar "|"  g,1 d1 g,1 \bar "|"  g,1 d1 g,1 \bar "||" \key g \minor g,1 d1 g,1 \bar "|"  g,1 d1 g,1 \bar "|"  g,1 d1 g,1 \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { \markup \tiny \italic "sol majeur" _ _ _ _ _ _ _ _ \markup \tiny \italic "sol mineur" _ _ _ _ _ _ _ _ }
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
