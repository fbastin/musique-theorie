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
    \new Staff = "haut" { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "md" { \key c \major <e' g' c''>1 <f' a' c''>1 <d' g' b'>1 <e' g' c''>1 \bar "|"  <g' c'' e''>1 <a' c'' f''>1 <g' b' d''>1 <g' c'' e''>1 \bar "|"  <c' e' g'>1 <c' f' a'>1 <b d' g'>1 <c' e' g'>1 \bar "||" \key c \minor <ees' g' c''>1 <f' aes' c''>1 <d' g' b'>1 <ees' g' c''>1 \bar "|"  <g' c'' ees''>1 <aes' c'' f''>1 <g' b' d''>1 <g' c'' ees''>1 \bar "|"  <c' ees' g'>1 <c' f' aes'>1 <b d' g'>1 <c' ees' g'>1 \bar "|." } }
    \new Staff { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key c \major c1 f1 g1 c1 \bar "|"  c1 f1 g1 c1 \bar "|"  c1 f1 g1 c1 \bar "||" \key c \minor c1 f1 g1 c1 \bar "|"  c1 f1 g1 c1 \bar "|"  c1 f1 g1 c1 \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { \markup \tiny \italic "do majeur" _ _ _ _ _ _ _ _ _ _ _ \markup \tiny \italic "do mineur" _ _ _ _ _ _ _ _ _ _ _ }
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
