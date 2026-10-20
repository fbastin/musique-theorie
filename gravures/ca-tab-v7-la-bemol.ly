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
    \new Staff = "haut" { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "md" { \key aes \major <c' ees' aes'>1 <des' ees' g'>1 <c' ees' aes'>1 \bar "|"  <ees' aes' c''>1 <ees' g' des''>1 <ees' aes' c''>1 \bar "|"  <aes' c'' ees''>1 <g' des'' ees''>1 <aes' c'' ees''>1 \bar "||" \key aes \minor <ces' ees' aes'>1 <des' ees' g'>1 <ces' ees' aes'>1 \bar "|"  <ees' aes' ces''>1 <ees' g' des''>1 <ees' aes' ces''>1 \bar "|"  <aes' ces'' ees''>1 <g' des'' ees''>1 <aes' ces'' ees''>1 \bar "|." } }
    \new Staff { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key aes \major aes,1 ees1 aes,1 \bar "|"  aes,1 ees1 aes,1 \bar "|"  aes,1 ees1 aes,1 \bar "||" \key aes \minor aes,1 ees1 aes,1 \bar "|"  aes,1 ees1 aes,1 \bar "|"  aes,1 ees1 aes,1 \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { \markup \tiny \italic "la bémol majeur" _ _ _ _ _ _ _ _ \markup \tiny \italic "la bémol mineur" _ _ _ _ _ _ _ _ }
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
