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
    \new Staff = "haut" { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "md" { \key bes \major <d' f' bes'>1 <ees' g' bes'>1 <c' f' a'>1 <d' f' bes'>1 \bar "|"  <f' bes' d''>1 <g' bes' ees''>1 <f' a' c''>1 <f' bes' d''>1 \bar "|"  <bes d' f'>1 <bes ees' g'>1 <a c' f'>1 <bes d' f'>1 \bar "||" \key bes \minor <des' f' bes'>1 <ees' ges' bes'>1 <c' f' a'>1 <des' f' bes'>1 \bar "|"  <f' bes' des''>1 <ges' bes' ees''>1 <f' a' c''>1 <f' bes' des''>1 \bar "|"  <bes des' f'>1 <bes ees' ges'>1 <a c' f'>1 <bes des' f'>1 \bar "|." } }
    \new Staff { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key bes \major bes,1 ees1 f1 bes,1 \bar "|"  bes,1 ees1 f1 bes,1 \bar "|"  bes,1 ees1 f1 bes,1 \bar "||" \key bes \minor bes,1 ees1 f1 bes,1 \bar "|"  bes,1 ees1 f1 bes,1 \bar "|"  bes,1 ees1 f1 bes,1 \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { \markup \tiny \italic "si bémol majeur" _ _ _ _ _ _ _ _ _ _ _ \markup \tiny \italic "si bémol mineur" _ _ _ _ _ _ _ _ _ _ _ }
    \context Lyrics = "positions" \lyricsto "md" { \markup \tiny \italic "octave" _ _ _ \markup \tiny \italic "tierce" _ _ _ \markup \tiny \italic "quinte" _ _ _ \markup \tiny \italic "octave" _ _ _ \markup \tiny \italic "tierce" _ _ _ \markup \tiny \italic "quinte" _ _ _ }
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
